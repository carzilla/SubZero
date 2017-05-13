import sys, re

def readsrt(filename, lasttoxic = False):
    last = -1
    if lasttoxic:
        last = -2
    print("Opening {}".format(filename))
    f = open(filename, 'r')
    srt = f.read()
    srt_list = srt.split('\n\n')
    while srt_list[last] == "":
        last = last -1
    print("\n\nPlease find the following line:\n")
    print(srt_list[last])
    found = input("\nWhere is this line? (hh:mm:ss format)")
    regex = r"(\d.:\d.:\d.)"
    found_list = found.split(":")
    last_line = srt_list[last].split('\n')
    timestamps = re.findall(regex, last_line[1])
    timestamps_list = timestamps[0].split(":")
    last_line_s = (int(timestamps_list[0]) * 3600) + (int(timestamps_list[1]) * 60) + int(timestamps_list[2])
    found_s = (int(found_list[0]) * 3600) + (int(found_list[1]) * 60) + int(found_list[2])
    offset = found_s - last_line_s
    offset_per_s = last_line_s / offset
    fixsrt(srt_list, offset_per_s)

def timestamp_to_s(timestamp):
    tmp = timestamp.split(":")
    return (int(tmp[0]) * 3600) + (int(tmp[1]) * 60) + (int(tmp[2]))

def s_to_timestamp(s):
    hours = s / 3600
    if hours < 1:
        hours = 0
    minutes = int(s / 60)
    if minutes > 60:
        minutes = 60

    tmp = (hours * 3600) + (minutes * 60)
    seconds = int(s - tmp)

    return "{:02d}:{:02d}:{:02d},000".format(hours, minutes, seconds)


def fixsrt(srt, offset_per_s):
    f = open('fixed.srt', 'w')
    regex = r"(\d.:\d.:\d.)"
    for item in srt:
        tmp = item.split("\n")
        new = tmp[0] + "\n"
        stamps = re.findall(regex, tmp[1])
        start = timestamp_to_s(stamps[0])
        end = timestamp_to_s(stamps[1])
        offset = start / offset_per_s
        new_start = s_to_timestamp(start + offset)
        new_end = s_to_timestamp(end + offset)
        new = new + new_start + " --> " + new_end + "\n"
        new = new + "\n".join(tmp[2:])
        new = new + "\n\n"
        f.write(new)
    f.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Needs SRT file input.")
        exit()
    if len(sys.argv) > 2:
        readsrt(sys.argv[1], True)
    else:
        readsrt(sys.argv[1])
