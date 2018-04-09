from __future__ import print_function
import coremltools
import keras

print('Convert the model to CoreML-Model ..')

#THIS SHOULD MATCH YOUR CLASSES !!!
#IT MEANS: Class 0 (in *.csv) is mapped as '0' and so on
output_labels = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9','A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
scale = 1/255.
coreml_model = coremltools.converters.keras.convert('./OCR_cnn.h5',
                                                    input_names='image',
                                                    image_input_names='image',
                                                    output_names='output',
                                                    class_labels=output_labels,
                                                    image_scale=scale)

#SOME ADDITIONAL INFOMARTION ABOUT YOR MODEL
coreml_model.author = 'DrNeurosurg'
coreml_model.license = 'MIT'
coreml_model.short_description = 'Model to classify characters (Font:INCONSOLATA)'

coreml_model.input_description['image'] = 'Grayscale image'
coreml_model.output_description['output'] = 'Predicted character'

# SAVE THE COREML.model for using in Xcode
coreml_model.save('OCR.mlmodel')

print('\n')
print('\n')
print('Trained with Keras Version', keras.__version__)
print('\n')