import psutil

def get_size_readable(size_bytes):
    # Convert size from bytes to KB, MB, GB, TB
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024

def get_storage_info():
    partitions = psutil.disk_partitions(all=True)
    storage_info = []
    
    for partition in partitions:
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
            info = {
                'device': partition.device,
                'mountpoint': partition.mountpoint,
                'fstype': partition.fstype,
                'total_size': get_size_readable(partition_usage.total),
                'used': get_size_readable(partition_usage.used),
                'free': get_size_readable(partition_usage.free),
                'percent_used': partition_usage.percent
            }
            storage_info.append(info)
        except PermissionError:
            # Some partitions might not be accessible due to permission errors
            pass
    
    return storage_info

if __name__ == "__main__":
    storage_info = get_storage_info()
    for info in storage_info:
        if info['device'] == "/dev/sdc" and info['mountpoint'] == "/":
            used_storage_percent = info['percent_used']
            print(100 - used_storage_percent)
