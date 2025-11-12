#!/usr/bin/env python3
import glob
import os
import re

# --- Configuration ---
output_filename = "merged_captions.txt"
file_glob_pattern = "*.vtt"  # Finds all .vtt files in the current folder
# ---------------------

# Find and sort the VTT files
# vtt_files = sorted(glob.glob(file_glob_pattern))
vtt_files = sorted(glob.glob(file_glob_pattern), key=lambda f: int(re.search(r'\d+', os.path.basename(f)).group()))

if not vtt_files:
    print(f"No files found matching '{file_glob_pattern}'.")
    exit()

print(f"Found {len(vtt_files)} files. Merging into '{output_filename}'...")

# Open the single output file
with open(output_filename, "w", encoding="utf-8") as outfile:
    for filename in vtt_files:
        print(f"Processing: {filename}")
        
        # Add a header to separate content from different files
        outfile.write(f"\n\n--- Source: {filename} ---\n\n")
        
        with open(filename, "r", encoding="utf-8") as infile:
            lines = infile.readlines()

        # This logic finds a timestamp, then joins all
        # subsequent text lines until it hits a blank line.
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Check if the line is a timestamp
            if "-->" in line:
                i += 1  # Move to the next line (the start of the caption)
                caption_block = []
                
                # Keep reading lines until we hit a blank one
                while i < len(lines) and lines[i].strip():
                    caption_block.append(lines[i].strip())
                    i += 1
                
                # If we found text, join it with spaces and write it
                if caption_block:
                    outfile.write(" ".join(caption_block) + "\n")
            else:
                # Not a timestamp, just move to the next line
                i += 1

print("\nDone! All VTT files have been merged.")
