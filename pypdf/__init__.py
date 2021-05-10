import os
import subprocess

from fileio import File
from pypdf.logger import get_logger

lib_root = os.path.abspath(os.path.dirname(__file__))
lib_paths = {
    'bin': File.join(lib_root, 'bin'),
    'jar': File.join(lib_root, 'bin', 'pdfact.jar'),
    'exec': File.join(lib_root, 'bin', 'pdfact'),
}
logger = get_logger()

from pypdf.utils import run_checks, call_module

_base_params = {
    'format': 'json',
    'units': ['paragraphs'],
    'include_roles': [
        'title','body', 'appendix', 'keywords', 'heading', 'general_terms', 'toc',
        'caption', 'table', 'other', 'categories', 'keywords', 'page_header'
    ],
    'visualize': None,
    'exclude_roles': None,
    'with_control_characters': False,
}

class PyPDF:
    def __init__(self, input_dir=None, output_dir=None, overwrite=True, **kwargs):
        self.params = _base_params.copy()
        if kwargs:
            self.params.update(**kwargs)
        self.overwrite = overwrite
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.extracted = {}
        run_checks()
    
    def update_paths(self, input_dir=None, output_dir=None):
        if input_dir:
            logger.info(f'Updating Input Dir: {self.input_dir} -> {input_dir}')
            self.input_dir = input_dir
        if output_dir:
            logger.info(f'Updating Output Dir: {self.output_dir} -> {output_dir}')
            self.output_dir = output_dir
    
    def update_params(self, overwrite=None, **kwargs):
        if overwrite is not None:
            self.overwrite = overwrite
        if kwargs:
            self.params.update(**kwargs)

    def extract_pdf(self, input_file, output_file, overwrite=None, params=None):
        overwrite = overwrite if overwrite is not None else self.overwrite
        _params = self.params.copy()
        if params:
            _params.update(params)
        if _params['visualize'] and isinstance(_params['visualize'], bool):
            _params['visualize'] = self.get_vis_path(self.get_dir(output_file), output_file)
        if not overwrite and File.exists(output_file):
            logger.error(f'Overwrite = {overwrite} and File Exists = {output_file}')
            return output_file
        res = call_module(input_file=input_file, output_file=output_file, **_params)
        if not output_file:
            return res
        return output_file

    def extract_dir(self, input_dir=None, output_dir=None, overwrite=None, remap_dict=None, remap_funct=None):
        input_dir = input_dir or self.input_dir
        output_dir = output_dir or self.output_dir
        filenames = self.gather_files(input_dir)
        logger.info(f'Extracting {len(filenames)} Files')
        logger.debug(f'{filenames}')
        for fname in filenames:
            logger.info(f'Extracting {fname}')
            if remap_dict:
                output_file = remap_dict.get(fname, None)
                if not output_file:
                    output_file = remap_dict.get(File.base(fname), None)
                assert output_file
            elif remap_funct:
                output_file = remap_funct(fname)
                assert output_file
            else:
                output_file = self.get_filepath(output_dir, fname) if output_dir else None
            res = self.extract_pdf(fname, output_file, overwrite)
            yield res
            self.extracted[fname] = res
        logger.info(f'Completed Extraction')
        self.extracted['params'] = self.params
        return self.extracted
    
    def extract(self, input_dir=None, output_dir=None, overwrite=None, remap_dict=None, remap_funct=None):
        return self.extract_dir(input_dir=input_dir, output_dir=output_dir, overwrite=overwrite, remap_dict=remap_dict, remap_funct=remap_funct)
    
    def get_filepath(self, output_dir, input_file):
        output_fn = File.base(input_file).split('.')[0] + '.' + self.params['format']
        return File.join(output_dir, output_fn)
    
    def get_vis_path(self, output_dir, output_file):
        output_fn = File.base(output_file).split('.')[0] + '_visual.pdf'
        return File.join(output_dir, output_fn)
    
    @classmethod
    def get_dir(cls, filepath):
        dir_path = os.path.abspath(os.path.dirname(filepath))
        File.mkdirs(dir_path)
        return dir_path

    def gather_files(self, input_dir):
        if not input_dir.endswith('.pdf'):
            if input_dir.endswith('*'):
                input_dir += '.pdf'
            elif input_dir.endswith('/'):
                input_dir += '*.pdf'
            else:
                input_dir += '/*.pdf'
        return File.glob(input_dir)

    def __call__(self, input_file, output_file=None, **kwargs):
        return call_module(input_file=input_file, output_file=output_file, **kwargs)
