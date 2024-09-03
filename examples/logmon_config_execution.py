import os


def get_total_memory_in_gb():
    memory_in_bytes = os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES")
    memory_in_gb = memory_in_bytes / pow(1024, 3)
    return memory_in_gb
