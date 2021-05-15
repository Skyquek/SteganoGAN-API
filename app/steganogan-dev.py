import torch
from steganogan import SteganoGAN

steganogan = SteganoGAN.load(architecture='dense', cuda=False, verbose=True)

print("encode")
steganogan.encode('static/original/input.png', 'static/output/output.png', '00966efaba812660d426a0f10542dadac919f6465dc0a87eac413f934bc0526a')

print("decode")
secretMsg = steganogan.decode('static/output/output.png')
print(secretMsg)