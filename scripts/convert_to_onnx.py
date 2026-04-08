import os
import subprocess
import shutil
import tensorflow as tf
import logging

logging.basicConfig(level=logging.ERROR)

def convert_model(keras_path, onnx_path):
    if not os.path.exists(keras_path):
        print(f"⚠️ Skipping {keras_path}, file not found.")
        return
    
    print(f"⏳ Loading TensorFlow model: {keras_path}...")
    model = tf.keras.models.load_model(keras_path, compile=False)
    
    temp_dir = "temp_tf_model_export"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
        
    print(f"⚙️ Exporting intermediate SavedModel to {temp_dir}...")
    try:
        model.export(temp_dir)
    except AttributeError:
        # Fallback for older TF versions
        model.save(temp_dir)
    
    print(f"⚙️ Converting via tf2onnx CLI...")
    cmd = [
        "python", "-m", "tf2onnx.convert",
        "--saved-model", temp_dir,
        "--output", onnx_path,
        "--opset", "15"
    ]
    subprocess.run(cmd, check=True)
    
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
        
    print(f"✅ Successfully created {onnx_path}\n")

if __name__ == "__main__":
    print("🚀 Starting ONNX Migration v2 (SavedModel Bypass)...")
    os.makedirs("models", exist_ok=True)
    
    convert_model("models/substation_model_v1.h5", "models/substation_model_v1.onnx")
    convert_model("models/substation_model_v2.h5", "models/substation_model_v2.onnx")
    convert_model("models/substation_model_v3_final.keras", "models/substation_model_v3_final.onnx")
    
    if os.path.exists("models/checkpoints/best_v3.keras"):
        os.makedirs("models/checkpoints", exist_ok=True)
        convert_model("models/checkpoints/best_v3.keras", "models/checkpoints/best_v3.onnx")
        
    print("🎉 All Models Converted to ONNX!")
