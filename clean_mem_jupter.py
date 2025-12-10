import psutil

mem = psutil.virtual_memory()
print(f"Total: {mem.total/1e9:.2f} GB")
print(f"Available: {mem.available/1e9:.2f} GB")
print(f"Used: {mem.used/1e9:.2f} GB")
print(f"Percent Used: {mem.percent}%")

