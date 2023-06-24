import subprocess
import logging
import sys
from shlex import join
from shlex import split

log0 = logging.getLogger(__name__)


class SubProcessHelper():

    class RunError(subprocess.CalledProcessError):
        pass

    @classmethod
    def decode(cls, bytearr):
        try:
            return bytearr.decode(encoding="utf-8")
        except Exception:
            pass
        return '[Non utf-8] ' + str(bytearr)

    @classmethod
    def run(cls, cmd: str | list | tuple, *args, outErrSink=None, log=None, shell=False, **kwargs):

        _log = log if log else log0

        def outErrSink0(out, err):
            if out:
                print(cls.decode(out).rstrip())
            if err:
                print(cls.decode(err).rstrip(), file=sys.stderr)

        _outErrSink = outErrSink if outErrSink else outErrSink0

        retcode = None

        def helper():
            nonlocal retcode

            _cmd = split(cmd) if isinstance(cmd, str) else list(cmd)
            _cmd = join(_cmd)
            _cmd = "stdbuf -oL -eL " + _cmd
            if not shell:
                _cmd = split(_cmd)
            pipes = subprocess.Popen(
                _cmd, *args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=shell, **kwargs)
            stdout, stderr = pipes.stdout, pipes.stderr
            retcode = None
            while (retcode is None):

                while True:
                    out = stdout.readline() if stdout else []
                    err = stderr.readline() if stderr else []

                    out = out if len(out) > 0 else None
                    err = err if len(err) > 0 else None

                    if not out is None or not err is None:
                        yield out, err
                    else:
                        break

                retcode = pipes.poll()

        for out, err in helper():
            _outErrSink(out, err)

        logf = _log.info if retcode == 0 else _log.error
        logf('{} returned {}.'.format(' '.join(cmd[0]), retcode))

        return retcode
