import cv2

def decode_text_from_image(image_path):
    img = cv2.imread(image_path)
    h, w, _ = img.shape
    text = ""

    # Iterate through image pixels to retrieve encoded text
    for i in range(h):
        for j in range(w):
            char = chr(img[i, j, 0])  # Retrieve ASCII value from the blue channel
            text += char

            if text.endswith("##END##"):
                return text.replace("##END##", "")

    return text
