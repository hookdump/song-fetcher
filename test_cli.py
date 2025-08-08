#!/usr/bin/env python3

import subprocess
import sys

# Test different command line options
test_commands = [
    ['python', 'main.py', '--help'],
    ['python', 'main.py', 'Pink Champagne'],
    ['python', 'main.py', '-o', '/tmp/music', 'In Christ Alone'],
]

print("Testing command line arguments:\n")

for cmd in test_commands:
    print(f"Command: {' '.join(cmd)}")
    print("-" * 50)
    
    # Run with immediate quit input
    result = subprocess.run(
        cmd, 
        input="q\n", 
        text=True, 
        capture_output=True,
        timeout=5
    )
    
    # Show first few lines of output
    lines = result.stdout.split('\n')[:15]
    for line in lines:
        if line:
            print(line)
    
    print("\n" + "=" * 60 + "\n")