from math import cos, sin, log, sqrt, atan, pi, acos
import numpy as np
from PIL import Image
import pickle
import random

publicKey = 356130857

def power(a, n, mod):
    ans = 1
    while n > 0:
        if n % 2 == 1: ans = (ans * a) % mod
        a = (a * a) % mod
        n //= 2
    return ans


def getKeyFromPassword(password):
    mod = 1000000007
    key = 0
    for c in password:
        key = (key * 256 + ord(c)) % mod
    return 10 + power(key, publicKey, mod)

def getComplexArrayFromDumpFile(fileName):
    file = open(fileName, 'rb')
    array, width, height = pickle.load(file)
    file.close()
    return array, width, height

def dumpComplexArray(array, width, height, fileName):
    file = open(fileName, 'wb')
    pickle.dump((array, width, height), file)
    file.close()

def getComplexArrayFromImage(fileName, extension):
    img = Image.open(fileName)
    width, height = img.size
    matrix = np.asarray(img)
    arraySize = 1
    while arraySize < width * height: arraySize *= 2
    array = [0 for i in range(arraySize)]
    for i in range(height):
        for j in range(width):
            array[width * i + j] = matrix[i, j][0] + matrix[i, j][1] * 256 + matrix[i, j][2] * 1j
            if extension == "png": array[width * i + j] += matrix[i, j][3] * 256j
    return (width, height, array)


def outputImageFromComplexArray(array, width, height, fileName, extension):
    if extension == "png": start = (0, 0, 0, 0)
    else: start = (0, 0, 0)
    matrix = np.zeros([height, width, 4 if extension == "png" else 3], dtype=np.uint8)
    allBlack = True
    for i in range(height):
        if not allBlack: break
        for j in range(width):
            real = abs(int(array[width * i + j].real))
            imag = abs(int(array[width * i + j].imag))
            if real != 0 or imag != 0:
                allBlack = False
                break
    for i in range(height):
        for j in range(width):
            real = abs(int(array[width * i + j].real))
            imag = abs(int(array[width * i + j].imag))
            r = real % 256
            g = (real // 256) % 256
            b = imag % 256
            if allBlack:
                r = random.randint(0, 255)
                g = random.randint(0, 255)
                b = random.randint(0, 255)
            a = (imag // 256) % 256
            if a < 100: a = 100
            if extension == "png": matrix[i, j] = [r, g, b, a]
            else: matrix[i, j] = [r, g, b]
    img = Image.fromarray(matrix)
    img.save(fileName)

def encryptComplex(c, key):
    key = cos(key)
    return c ** key

def decryptComplex(c, key):
    key = cos(key)
    return c ** (1/key)