import multiprocessing
import time

# Fungsi untuk menghitung total harga pembelian semua pelanggan
def count_total_price(price_queue, total_price):
    while True:
        # Ambil harga dari antrian
        price = price_queue.get()

        # Jika harga adalah -1, artinya tidak ada pembelian lagi
        if price == -1:
            break

        # Tambahkan harga ke total harga
        total_price.value += price

# Fungsi untuk memproses pembelian
def process_purchase(price_queue, customer_name, shoe_size, shoe_price):
    # Simulasi proses pembelian
    print(f"{customer_name} membeli sepatu ukuran {shoe_size} dengan harga {shoe_price}")
    start_time = time.time()
    time.sleep(1) # tunggu selama 1 detik
    end_time = time.time()

    # Hitung harga total pembelian
    total_price = shoe_price * 1.1  # Tambahkan 10% pajak
    price_queue.put(total_price)

    # Cetak waktu pemrosesan
    print(f"Waktu pemrosesan {customer_name}: {end_time - start_time:.2f} detik")

if __name__ == '__main__':
    # Inisialisasi queue dan shared variable
    price_queue = multiprocessing.Queue()
    total_price = multiprocessing.Value('f', 0)

    # Buat proses induk untuk menghitung total harga pembelian
    price_process = multiprocessing.Process(target=count_total_price, args=(price_queue, total_price))
    price_process.start()

    # Memunculkan proses anak untuk memproses pembelian pelanggan
    processes = []
    for purchase in [("Andi", 40, 400), ("Budi", 42, 125), ("Cindy", 38, 155)]:
        p = multiprocessing.Process(target=process_purchase, args=(price_queue, purchase[0], purchase[1], purchase[2]))
        processes.append(p)
        p.start()

    # Tunggu sampai semua proses anak selesai
    for p in processes:
        p.join()

    # Tandai akhir pembelian
    price_queue.put(-1)

    # Tunggu sampai proses parent selesai menghitung total harga pembelian
    price_process.join()

    # Cetak total harga pembelian
    print(f"Total harga pembelian: {total_price.value}")
