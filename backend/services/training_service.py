def trigger_training_pipeline():
    # logic này có thể là gọi subprocess hoặc API nội bộ để chạy training
    import subprocess
    try:
        result = subprocess.run(["python", "scripts/train.py"], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return f"⚠️ Lỗi khi chạy training pipeline: {e}"