
import os
import sys
import subprocess

from pypdf import logger, lib_paths, File

_jdk_path = os.environ.get('JAVA_HOME', None)
_module_exist = File.exists(lib_paths['jar'])
_module_paths = {
    'jar': 'https://github.com/ad-freiburg/pdfact/raw/master/bin/pdfact.jar',
    'exec': 'https://github.com/ad-freiburg/pdfact/raw/master/bin/pdfact'
}


def exec_command(cmd):
    out = subprocess.check_output(cmd, shell=True)
    if isinstance(out, bytes):
        out = out.decode('utf8')
    return out.strip()


def get_variable_separator():
    """
    Returns the environment variable separator for the current platform.
    :return: Environment variable separator
    """
    if sys.platform.startswith('win'):
        return ';'
    return ':'


def find_binary_in_path(filename):
    """
    Searches for a binary named `filename` in the current PATH. If an executable is found, its absolute path is returned
    else None.
    :param filename: Filename of the binary
    :return: Absolute path or None
    """
    if 'PATH' not in os.environ:
        return None
    for directory in os.environ['PATH'].split(get_variable_separator()):
        binary = os.path.abspath(os.path.join(directory, filename))
        if os.path.isfile(binary) and os.access(binary, os.X_OK):
            return binary
    return None

def call_module(input_file, output_file=None, **kwargs):
    call_args = ['java', '-jar', lib_paths['jar']]
    for k,v in kwargs.items():
        if v is None:
            continue
        k = k.replace('_', '-')
        if isinstance(v, bool):
            if v:
                call_args.append(f'--{k}')
        else:
            if isinstance(v, list):
                v = ','.join(v)
            v = v.replace('_', '-')
            call_args.extend([f'--{k}', v])
    call_args.append(input_file)
    if output_file:
        call_args.append(output_file)
    logger.debug(f'Call Args: {call_args}')
    return subprocess.call(call_args)


def run_checks():
    global _jdk_path, _module_exist
    if not _module_exist:
        logger.debug(f'Getting Module')
        File.absdownload(_module_paths['jar'], filepath=lib_paths['jar'])
        _module_exist = True

    if not _jdk_path:
        _check_jdk = exec_command('which java')
        if _check_jdk and 'java' in _check_jdk:
            logger.debug(f'Setting JAVA_HOME to {_check_jdk}')
            os.environ['JAVA_HOME'] = _check_jdk
            _jdk_path = _check_jdk
        else:
            logger.warn(f'Java was not found in Environment Variables. This may cause problems.')
            return
    if _jdk_path not in os.environ['PATH']:
        logger.debug(f'Appending {_jdk_path} to PATH')
        sys.path.append(_jdk_path)
    return bool(_jdk_path and _module_exist)
    

