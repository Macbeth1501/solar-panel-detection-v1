from ultralytics import YOLO

# Load the saved YOLOv8 model
model = YOLO('final_model.pt')

# Path to the image you want to perform predictions on
image_path = r"C:\Users\Rochan\Desktop\Coding\Micro_Project_2\test\images\7_png.rf.9d7644440f70c7c0fef92098207fa1e5.jpg"

# Run inference on the image
results = model(image_path)

# If results is a list, access the first element and display it
if isinstance(results, list):
    # Display the first result in the list
    results[0].show()
else:
    # If it's not a list, you can directly use .show() on the result
    results.show()


