#!/usr/bin/env python3
"""
Test CSV file accessibility and basic operations
"""

import pandas as pd
import os
from pathlib import Path

def test_csv_access():
    """Test if finalapi.csv is accessible and readable"""
    csv_file = 'finalapi.csv'
    
    print("🔍 Testing CSV file accessibility...")
    print("=" * 50)
    
    # Check if file exists
    if not os.path.exists(csv_file):
        print(f"❌ Error: {csv_file} not found")
        print("Available CSV files:")
        csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]
        if csv_files:
            for f in csv_files:
                print(f"  📄 {f}")
        else:
            print("  No CSV files found in current directory")
        return False
    
    # Check file size
    file_size = os.path.getsize(csv_file)
    print(f"📄 File: {csv_file}")
    print(f"📊 Size: {file_size:,} bytes ({file_size / 1024 / 1024:.2f} MB)")
    
    # Try to read the file
    try:
        print("📖 Attempting to read CSV file...")
        df = pd.read_csv(csv_file)
        
        print(f"✅ Successfully loaded CSV file!")
        print(f"📏 Shape: {df.shape[0]:,} rows × {df.shape[1]:,} columns")
        
        # Show first few columns and rows
        print(f"\n🔍 First 5 columns: {list(df.columns[:5])}")
        print(f"🔍 Sample data:")
        print(df.head(3).to_string(max_cols=5))
        
        # Check for missing values
        missing_count = df.isnull().sum().sum()
        print(f"\n📊 Missing values: {missing_count:,}")
        
        # Check for 99999 placeholder values
        placeholder_count = (df == 99999).sum().sum()
        print(f"📊 Placeholder values (99999): {placeholder_count:,}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error reading CSV file: {e}")
        return False

def test_output_directories():
    """Test if output directories can be created"""
    print("\n🗂️ Testing output directory creation...")
    
    try:
        # Create agent_comm directory
        output_dir = Path('agent_comm')
        output_dir.mkdir(exist_ok=True)
        print(f"✅ Created/verified: {output_dir}")
        
        # Create charts subdirectory
        charts_dir = output_dir / 'charts'
        charts_dir.mkdir(exist_ok=True)
        print(f"✅ Created/verified: {charts_dir}")
        
        # Test writing a simple file
        test_file = output_dir / 'test_write.txt'
        with open(test_file, 'w') as f:
            f.write("Test write successful")
        
        # Clean up test file
        test_file.unlink()
        print("✅ Write permissions confirmed")
        
        return True
        
    except Exception as e:
        print(f"❌ Error with directories: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 CSV ACCESS AND SETUP TESTS")
    print("=" * 60)
    
    # Test CSV access
    csv_ok = test_csv_access()
    
    # Test directories
    dir_ok = test_output_directories()
    
    print("\n" + "=" * 60)
    print("📋 TEST SUMMARY")
    print("=" * 60)
    print(f"CSV File Access: {'✅ PASS' if csv_ok else '❌ FAIL'}")
    print(f"Directory Setup: {'✅ PASS' if dir_ok else '❌ FAIL'}")
    
    if csv_ok and dir_ok:
        print("\n🎉 All tests passed! Your setup is ready for CSV analysis.")
    else:
        print("\n⚠️ Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main()