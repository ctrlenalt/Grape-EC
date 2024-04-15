# Notice

This is a repository for the AD/AE phase of [SC'24](https://sc24.supercomputing.org/) for the paper titled "GRAPE: Eliminating the Redundant Encoding/Decoding Computations of
Reed-Solomon Codes via Fine-grained Algebraic Operations".

About the latest version of this library, please visit the author's repository: https://github.com/ctrlenalt/Grape-EC.



# For benchmarking ISA-L
Please see the note: [HOWTO_BENCHMARK_ISAL.md](HOWTO_BENCHMARK_ISAL.md)

# For benchmarking SLP-EC
Please see the note: [HOWTO_BENCHMARK_ISAL.md](HOWTO_BENCHMARK_SLP_EC.md)

# For benchmarking ZCRS
Please see the note: [HOWTO_BENCHMARK_ISAL.md](HOWTO_BENCHMARK_ZCRS.md)

# For benchmarking ECRS
Please see the note: [HOWTO_BENCHMARK_ISAL.md](HOWTO_BENCHMARK_ECRS.md)




# For benchmarking Our Library

We need Rust https://www.rust-lang.org/.

If you have not installed Rust, please see the official instruction: https://www.rust-lang.org/tools/install

## Build
```
$ git clone https://github.com/ctrlenalt/Grape-EC
$ cd Grape-EC;
$ cargo build --release
$ ./target/release/xorslp_ec --help
xorslp_ec 0.1.0

USAGE:
    xorslp_ec [FLAGS] [OPTIONS]

FLAGS:
        --all-stat
    -h, --help           Prints help information
        --no-compress
        --stat-enc
    -V, --version        Prints version information

OPTIONS:
        --data-block <data-block>
        --enc-dec <enc-dec>...
        --loop-iter <loop-iter>
        --optimize-level <optimize-level>     [default: FusionSchedule]  [possible values: Nooptim, Fusion,
                                             FusionSchedule]
        --parity-block <parity-block>
        --stat-dec <stat-dec>...
```
 

The script "grape-matrix-w=8.py" is used to generate the encoding matrix for Grape. By modifying the parameters k and r in the main() function, different RS(k,r) encoding parameter matrices can be generated. Subsequently, the corresponding "k-r-8ring_matrix.csv" CSV file can be created. The purpose of this script is to generate encoding matrices based on different RS encoding parameters and save the results as CSV files for further analysis and application.
```
Execute the command: python3  grape-matrix-w=8.py


```
##Select different RS(k,r) encoding configurations

By modifying the "fn main()" function in the "main.rs" file, you can change the line "let file_path = "../Grape-slp-ec/6-3-8ring_matrix.csv";" to test Grape's encoding and decoding effects under different encoding parameters. For example, selecting the "6-3-8ring_matrix.csv" file allows you to test the RS(6,3) encoding and decoding effects. If you choose different files, such as "7-3-8ring_matrix.csv" to "100-3-8ring_matrix.csv" representing different Grape encoding matrices with RS(k,r) parameters, you can test the encoding and decoding scenarios from RS(7,3) to RS(100,3). This way, you can choose different encoding parameter files as needed to test the encoding and decoding effects of the corresponding RS code


## Benchmarking Encoding and Decoding
For **RS(6, 3)**：
For RS(6,3) encoding parameters, we choose to set the file path as "../Grape-slp-ec/6-3-8ring_matrix.csv". After saving the modifications, compile by running the "cargo build --release" command. Once the compilation is complete, proceed with the following steps:
```
./target/release/xorslp_ec --enc-dec --data-block 6 --parity-block 3
Block size = 2048
Benchmarking of Encoding & Decoding (with [2, 4, 5])
Encode: avg = 6730.219277859085 MB/s, sd = 588.1810438266632
Decode: avg = 3969.264539513236 MB/s, sd = 359.0427361915413

```
For **RS(100, 3)**：
For RS(100,3) encoding parameters, we choose to set the file path as "../Grape-slp-ec/100-3-8ring_matrix.csv". After saving the modifications, compile by running the "cargo build --release" command. Once the compilation is complete, proceed with the following steps:
```
./target/release/xorslp_ec --enc-dec --data-block 100 --parity-block 3
Block size = 2048
Benchmarking of Encoding & Decoding (with [2, 4, 5])
Encode: avg = 5952.949881780267 MB/s, sd = 139.4754898646716
Decode: avg = 4356.131332243102 MB/s, sd = 78.08672136641981

```
##Count the XOR operations during encoding：

Taking RS(6,3) as an example, to count the XOR operations during encoding, execute the following command: ./target/release/xorslp_ec --stat-enc --enc-dec --data-block 6 --parity-block 3. This command will track the number of XOR operations during encoding and also perform encoding and decoding operations simultaneously.
```
./target/release/xorslp_ec --stat-enc --enc-dec --data-block 6 --parity-block 3
Block size = 2048
Statistics for Encoding
[WithOUT comp.] #XOR = 102, #MemAcc = 306, #[Fusioned]MemAcc = 178,
  #[NoFusion]CacheTrans = 308, #[Fusioned]CacheTrans = 306, #[Fusioned&Scheduled]CacheTrans = 194,
  #[NoFusion]Variables = 38, #[Fusioned]Variables = 38, #[Fusioned&Scheduled]Variables = 38,
  #[NoFusion]Capacity = 77, #[Fusioned]Capacity = 77, #[Fusioned&Scheduled]Capacity = 76,
  #Statements = 38
[With comp.] #XOR = 98, #MemAcc = 294, #[Fusioned]MemAcc = 180,
  #[NoFusion]CacheTrans = 356, #[Fusioned]CacheTrans = 275, #[Fusioned&Scheduled]CacheTrans = 200,
  #[NoFusion]Variables = 98, #[Fusioned]Variables = 41, #[Fusioned&Scheduled]Variables = 38,
  #[NoFusion]Capacity = 104, #[Fusioned]Capacity = 86, #[Fusioned&Scheduled]Capacity = 83,
  #Statements = 41

```
 ##Count the XOR operations during decoding：

Taking RS(6,3) as an example, to count the XOR operations during decoding, execute the following command: ./target/release/xorslp_ec --enc-dec --data-block 6 --parity-block 3 --stat-dec 1 2 3. This command will track the number of XOR operations during decoding while performing encoding and decoding operations simultaneously.
```
./target/release/xorslp_ec --enc-dec --data-block 6 --parity-block 3 --stat-dec 1 2 3

Block size = 2048
Statistics for Decoding: [1, 2, 3]
[WithOUT comp.] #XOR = 474, #MemAcc = 1422, #[Fusioned]MemAcc = 522,
  #[NoFusion]CacheTrans = 1010, #[Fusioned]CacheTrans = 1004, #[Fusioned&Scheduled]CacheTrans = 602,
  #[NoFusion]Variables = 24, #[Fusioned]Variables = 24, #[Fusioned&Scheduled]Variables = 24,
  #[NoFusion]Capacity = 61, #[Fusioned]Capacity = 60, #[Fusioned&Scheduled]Capacity = 61,
  #Statements = 24
[With comp.] #XOR = 217, #MemAcc = 651, #[Fusioned]MemAcc = 405,
  #[NoFusion]CacheTrans = 871, #[Fusioned]CacheTrans = 658, #[Fusioned&Scheduled]CacheTrans = 457,
  #[NoFusion]Variables = 217, #[Fusioned]Variables = 94, #[Fusioned&Scheduled]Variables = 48,
  #[NoFusion]Capacity = 263, #[Fusioned]Capacity = 140, #[Fusioned&Scheduled]Capacity = 96,
  #Statements = 94


```
```
We can obtain all the statistics by the one command
Execute the command:  ./target/release/xorslp_ec --all-stat
```
./target/release/xorslp_ec --all-stat

[WithOUT comp.] #XOR = 916, #MemAcc = 2748, #[Fusioned]MemAcc = 964,
  #[NoFusion]CacheTrans = 1896, #[Fusioned]CacheTrans = 1896, #[Fusioned&Scheduled]CacheTrans = 1432,
  #[NoFusion]Variables = 24, #[Fusioned]Variables = 24, #[Fusioned&Scheduled]Variables = 24,
  #[NoFusion]Capacity = 93, #[Fusioned]Capacity = 92, #[Fusioned&Scheduled]Capacity = 91,
  #Statements = 24
[With comp.] #XOR = 384, #MemAcc = 1152, #[Fusioned]MemAcc = 692,
  #[NoFusion]CacheTrans = 1650, #[Fusioned]CacheTrans = 1184, #[Fusioned&Scheduled]CacheTrans = 871,
  #[NoFusion]Variables = 384, #[Fusioned]Variables = 154, #[Fusioned&Scheduled]Variables = 96,
  #[NoFusion]Capacity = 458, #[Fusioned]Capacity = 230, #[Fusioned&Scheduled]Capacity = 176,
  #Statements = 154
Dec [0, 1, 3, 4]:
[WithOUT comp.] #XOR = 1354, #MemAcc = 4062, #[Fusioned]MemAcc = 1418,
  #[NoFusion]CacheTrans = 2796, #[Fusioned]CacheTrans = 2796, #[Fusioned&Scheduled]CacheTrans = 2098,
  #[NoFusion]Variables = 32, #[Fusioned]Variables = 32, #[Fusioned&Scheduled]Variables = 32,
  #[NoFusion]Capacity = 88, #[Fusioned]Capacity = 87, #[Fusioned&Scheduled]Capacity = 90,




 
