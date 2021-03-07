import os
import sys
import shutil
import subprocess
from subprocess import PIPE

# def converter(input_dir, max_dir, mean_dir):
def converter(input_dir, max_dir):
    proc_getFile = subprocess.Popen(["ls", str(input_dir)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    vol_dict = {}
    for files in str(proc_getFile.stdout.read()).split("\n"):
        if len(files) != 0:
            proc_maxVolume = subprocess.Popen(
                ["ffmpeg", "-i", str(input_dir)+"/" + str(files), "-vn", "-af", "volumedetect", "-f", "null", "-"], 
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = str(proc_maxVolume.stderr.read())
            output_mean = output.split("mean_volume: ")[1].split(" dB")[0]
            output_max = output.split("max_volume: ")[1].split(" dB")[0]
            vol_dict[files] = {"mean":output_mean,"max":output_max}

    for i in vol_dict:
        print(i)
        print(vol_dict[i])

        max_val = vol_dict[i]["max"]
        if max_val != "0.0":
            if os.path.exists(str(max_dir)):
                pass
            else:
                os.mkdir(str(max_dir))
                
            if "-" in max_val:
                calc_val = max_val.split("-")[1]
            else:
                calc_val = "-"+str(max_val)

            proc_maxVolume = subprocess.Popen(
                ["ffmpeg", "-i", "{}/{}".format(str(input_dir),str(i)), "-vcodec", "copy" ,"-af", 'volume={}dB'.format(calc_val), "{}/modified_{}".format(str(max_dir),str(i))], 
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(proc_maxVolume.stdout.read())
            print(proc_maxVolume.stderr.read())
        else:
            shutil.copyfile("{}/{}".format(str(input_dir),str(i)), "{}/{}".format(str(max_dir),str(i)))
    
        # mean_val = vol_dict[i]["mean"]
        # if mean_val != "0.0":
        #     if os.path.exists(str(mean_dir)):
        #         pass
        #     else:
        #         os.mkdir(str(mean_dir))
            
        #     # calcuration based on mean
        #     if "-" in mean_val:
        #         calc_val = mean_val.split("-")[1]
        #     else:
        #         calc_val = "-"+str(mean_val)
        #     # calcuration based on min
        #     # if "-" in mean_val and "-" in max_val:
        #     #     calc_val = float(mean_val.split("-")[1])*2 - float(max_val.split("-")[1])
        #     # else:
        #     #     calc_val = float(mean_val.split("-")[1])*2 - float(max_val)
            

        #     print(calc_val)
        #     proc_meanVolume = subprocess.Popen(
        #         ["ffmpeg", "-i", "{}/{}".format(str(input_dir),str(i)), "-vcodec", "copy" ,"-af", 'volume={}dB'.format(str(calc_val)), "{}/modified_{}".format(str(mean_dir),str(i))], 
        #         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #     print(proc_meanVolume.stdout.read())
        #     print(proc_meanVolume.stderr.read())
        # else:
        #     shutil.copyfile("{}/{}".format(str(input_dir),str(i)), "{}/{}".format(str(mean_dir),str(i)))

def main():
    args = sys.argv
    input_dir = args[1]
    max_dir = args[2]
    # mean_dir = args[3]

    converter(input_dir, max_dir)

if __name__ == "__main__":
    main()