import json
import glob
from pathlib import Path

def extract_metadata_from_files() -> list[dict]:


    input_folder = Path("metadata")
    output_folder = Path("inputavaa")
    
    
    cwd = Path.cwd()
    

    input_exists = input_folder.exists()
    output_exists = output_folder.exists()

    input_folder.mkdir(exist_ok=True)
    output_folder.mkdir(exist_ok=True)
    
    print(f"Working directory: {cwd}")
    print(f"Input folder: {input_folder}")
    print(f"Output folder: {output_folder}")

    if not input_exists or not output_exists:
        print("\nFolders created.")
        print("Add JSON files to the 'metadata' folder and run the script again.")
        return []
    

    json_files = glob.glob(str(input_folder / "*.json"))
    
    if not json_files:
        print(f"No JSON files found in {input_folder}")
        print("Add JSON files to the 'metadata' folder and run the script again.")
        return []
    
  
    video_fields_to_remove = {
        "mentions", "music_id", "schedule_time", "location_created", "is_ad",
        "suggested_words", "diggcount", "sharecount", "commentcount", "playcount",
        "collectcount", "repostcount", "warn_info", "original_item", "offical_item",
        "secret", "for_friend", "digged", "item_comment_status", "take_down",
        "effect_stickers", "private_item", "duet_enabled", "stitch_enabled",
        "stickers_on_item", "share_enabled", "comments", "duet_display",
        "stitch_display", "index_enabled", "diversification_labels",
        "diversification_id", "channel_tags", "keyword_tags", "is_ai_gc",
        "aigc_label_type", "ai_gc_description"
    }
    

    music_fields_to_remove = {
        "original", "schedule_search_time", "collected", "precise_duration"
    }
    
    results = []
    
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
       
            video_metadata = data.get("video_metadata", {})
            music_metadata = data.get("music_metadata", {})
            
          
            filtered_video_metadata = {
                k: v for k, v in video_metadata.items() 
                if k not in video_fields_to_remove
            }
            
    
            filtered_music_metadata = {
                k: v for k, v in music_metadata.items() 
                if k not in music_fields_to_remove
            }
            
     
            video_id = filtered_video_metadata.get("id", "unknown_id")
            output_filename = f"{video_id}_avaainput.json"
            output_path = output_folder / output_filename
            
    
            combined_data = {
                "video_metadata": filtered_video_metadata,
                "music_metadata": filtered_music_metadata
            }
            
       
            with open(output_path, 'w', encoding='utf-8') as out_file:
                json.dump(combined_data, out_file, indent=2)
            
        
            file_result = {
                "filename": Path(json_file).name,
                "output_filename": output_filename,
                "video_metadata": filtered_video_metadata,
                "music_metadata": filtered_music_metadata
            }
            
            results.append(file_result)
            print(f"Processed and saved: {output_filename}")
            
        except FileNotFoundError:
            print(f"Error: File {json_file} not found")
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in {json_file}")
        except KeyError as e:
            print(f"Error: Missing expected key {e} in {json_file}")
        except Exception as e:
            print(f"Unexpected error processing {json_file}: {e}")
    
    return results


if __name__ == "__main__":
    print("Starting metadata extraction process...")
    

    extracted_data = extract_metadata_from_files()

    if extracted_data:
        print(f"\nSuccessfully processed {len(extracted_data)} files:")
        for item in extracted_data:
            print(f"  - {item['filename']} → {item['output_filename']}")
    else:
        print("\nNo files were processed. Check the messages above for details.")