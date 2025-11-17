def main():
    print("="*80)
    print("COMPLETE ETL PROCESS")
    print("="*80)
    print()
    
    print("STEP 1: Creating Database Schema")
    from create_schema import execute_schema
    if not execute_schema():
        print("\nSchema creation failed!")
        return False
    
    print("STEP 2: Running ETL Pipeline")
    from etl_pipeline import ETLPipeline
    pipeline = ETLPipeline()
    if not pipeline.run():
        print("\nETL pipeline failed!")
        return False
    
    print("ALL STEPS COMPLETED SUCCESSFULLY!")
    
    return True

if __name__ == "__main__":
    main()