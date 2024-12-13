import threading, time, os, subprocess

def compress_pdf(input_path, output_path, quality='screen'):
    commands = [
        'gs', '-sDEVICE=pdfwrite',
        '-dCompatibilityLevel=1.4',
        '-dPDFSETTINGS=/' + quality, # screen, ebook, printer, prepress, default
        '-dNOPAUSE', '-dBATCH', '-dQUIET',
        f'-sOutputFile={output_path}',
        input_path
    ]
    try:
        subprocess.run(commands, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return False

def schedule_file_deletion(file_path, delay=1800):
    def delete_file():
        time.sleep(delay)
        if os.path.exists(file_path):
            os.remove(file_path)
    threading.Thread(target=delete_file, daemon=True).start()
