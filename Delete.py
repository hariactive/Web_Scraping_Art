import os

def delete_alternate_images(folder_path):
    image_files = os.listdir(folder_path)
    image_files.sort()  # Sort the images in alphabetical order

    # Delete alternate images based on index (1, 3, 5, etc.)
    for i in range(1, len(image_files), 2):
        try:
            os.remove(os.path.join(folder_path, image_files[i]))
            print(f"Deleted: {image_files[i]}")
        except Exception as e:
            print(f"Error deleting {image_files[i]}: {e}")

# Replace 'images' with the path to your images folder
folder_path = 'Brave_images'
delete_alternate_images(folder_path)
