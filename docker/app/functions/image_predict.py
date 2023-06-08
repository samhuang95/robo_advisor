from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np

model = load_model('/app/model/image_predict.h5')

def predict_image(path):
  img = Image.open(path)
  img = img.convert('RGB')
  img = img.resize((224, 224))
  img = np.array(img)/255.
  img = np.expand_dims(img, axis=0)

  predictions = model.predict(img)
  predicted_labels = np.argmax(predictions[0], axis=-1)

  match predicted_labels:
    case 0: return 'C'
    case 1: return 'B'
    case 2: return 'A'
    case 3: return 'S'

if __name__ == '__main__':
  pass
