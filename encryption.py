import cv2
import os

def encode_text_in_image(image_path, text):
    img = cv2.imread(image_path)
    h, w, _ = img.shape
    text += "##END##"  # End marker for retrieval

    index = 0
    for i in range(h):
        for j in range(w):
            if index < len(text):
                img[i, j, 0] = ord(text[index])  # Store character ASCII in the blue channel
                index += 1
            else:
                break  # Exit if all text is encoded

        if index >= len(text):  # Exit outer loop once all text is encoded
            break

    # Save the encrypted image next to the original image
    encrypted_img_path = os.path.join(os.path.dirname(image_path), "encrypted.png")
    cv2.imwrite(encrypted_img_path, img)
    return encrypted_img_path
