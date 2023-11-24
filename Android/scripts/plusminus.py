# Define parameters for finding the point
def script(pixel_values):
    start_point = None
    max_range = 20  # Maximum range for the spike not to come down
    # Find the point where the spike goes up but doesn't come down within the maximum range
    nl = None
    for y in range(1, 700):
        sub = int(pixel_values[y])
        for z in range(3, 78):
            if int(pixel_values[(y+z)])-sub > 30:

                continue
            else:
                nl = True
                break

        if nl == False:
            start_point = y
            break
        else:
            nl = False
    # print(start_point)

    # Define parameters for spike detection
    min_amplitude = 10  # Minimum amplitude in pixels
    spike_detected = False
    spike_start = None
    spike_end = None
    spike_max_peaks = []
    spike_max_amplitudes = []

    # Detect spikes and find max peaks
    for y in range(15, start_point):

        if not spike_detected and pixel_values[y] > pixel_values[y - 1]:
            spike_detected = True
            spike_start = y
         #    print(spike_start)
        elif spike_detected and pixel_values[y] < pixel_values[y - 1]:
            spike_end = y
         #    print(spike_end)
            spike_detected = False
            spike_amplitude = max(
                pixel_values[spike_start:spike_end]) - min(pixel_values[spike_start:spike_end])
         #    print(max(pixel_values[spike_start:spike_end]),min(pixel_values[spike_start:spike_end]))

         #    print(spike_amplitude >= min_amplitude and spike_width <= max_width)
            if spike_amplitude >= min_amplitude:
                max_peak_index = spike_start + \
                    pixel_values[spike_start:spike_end].index(
                        max(pixel_values[spike_start:spike_end]))

                spike_max_peaks.append(max_peak_index)
                spike_max_amplitudes.append(spike_amplitude)

    while len(spike_max_peaks) > 5:
        index_min = spike_max_amplitudes.index(min(spike_max_amplitudes))
        spike_max_peaks.pop(index_min)
        spike_max_amplitudes.pop(index_min)

    return spike_max_peaks    