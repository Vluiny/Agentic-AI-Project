from langchain_core.tools import tool

@tool
def time() -> str:
    """Gunakan tool ini jika user menanyakan jam, waktu, atau tanggal hari ini."""
    import datetime
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")