import os
import threading

def split_file(input_file, output_prefix, num_parts):
    # 입력 파일의 크기를 가져옵니다.
    file_size = os.path.getsize(input_file)
    part_size = file_size // num_parts

    # 청크 크기를 설정합니다 (예: 100MB)
    chunk_size = 100 * 1024 * 1024

    with open(input_file, 'rb') as f_in:
        for i in range(num_parts):
            output_file = f"{output_prefix}_part{i+1}.log"
            with open(output_file, 'wb') as f_out:
                bytes_written = 0
                while bytes_written < part_size:
                    remaining = part_size - bytes_written
                    read_size = min(chunk_size, remaining)
                    data = f_in.read(read_size)
                    if not data:
                        break
                    f_out.write(data)
                    bytes_written += len(data)

        # 만약 나머지 데이터가 있다면 마지막 파일에 씁니다.
        remaining_data = f_in.read()
        if remaining_data:
            with open(f"{output_prefix}_part{num_parts}.log", 'ab') as f_out:
                f_out.write(remaining_data)

def split_files_in_parallel():
    # 두 개의 파일을 각각 나누는 작업을 스레드로 실행
    thread1 = threading.Thread(target=split_file, args=('strace1.log', 'strace1', 20))
    thread2 = threading.Thread(target=split_file, args=('strace.log', 'strace', 20))

    # 두 스레드를 시작
    thread1.start()
    thread2.start()

    # 두 스레드가 작업을 완료할 때까지 기다림
    thread1.join()
    thread2.join()

# 병렬로 파일 분할 실행
split_files_in_parallel()

