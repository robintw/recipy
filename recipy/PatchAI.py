import sys
from .PatchImporter import PatchImporter
from .PatchSimple import PatchSimple
from .PatchMultipleWrappers import PatchMultipleWrappers, WrapperList

from .log import log_input, log_output, add_module_to_db
from recipyCommon.utils import create_wrapper, multiple_insert

class PatchKeras(PatchSimple):
    modulename = 'keras'

    wrappers = WrapperList()

    datasets = ['datasets.imdb', 'datasets.reuters', 'datasets.mnist', 'datasets.boston_housing']

    input_functions = [ds + '.load_data' for ds in datasets]

    input_functions += ['Model.load_weights', 'ImageDataGenerator.flow_from_directory']

    input_functions += ['preprocessing.image.load_img']

    input_functions += ['utils.HDF5Matrix', 'utils.get_file']

    output_functions = ['Model.save_weights', 'Model.save']
    output_functions += ['callbacks.ModelCheckpoint', 'callbacks.CSVLogger']

    wrappers.add_inputs(input_functions, log_input, 0, modulename)
    wrappers.add_outputs(output_functions, log_output, 0, modulename)
    wrappers.add_outputs('utils.plot_model', log_output, 1, modulename)

    add_module_to_db(modulename, input_functions, output_functions)

multiple_insert(sys.meta_path, [PatchKeras()])