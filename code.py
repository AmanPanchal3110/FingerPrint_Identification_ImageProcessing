import cv2
import os

# --- 1. Improved Logic: Returns Score AND Visual Data ---
def get_match_details(img1, img2):
    # Initialize SIFT
    sift = cv2.SIFT_create()
    
    # Keypoints and Descriptors
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)
    
    # Safety check
    if des1 is None or des2 is None:
        return 0, None, None, None

    # FLANN Matcher
    index_params = dict(algorithm=1, trees=10)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    
    matches = flann.knnMatch(des1, des2, k=2)
    
    # Lowe's Ratio Test
    good_points = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good_points.append(m)
            
    # Return: Score, Keypoints1, Keypoints2, The List of Matches
    return len(good_points), kp1, kp2, good_points

# --- 2. Helper to Show Images ---
def show_comparison(title, img1, kp1, img2, kp2, matches):
    # Draw the matches
    result_img = cv2.drawMatches(img1, kp1, img2, kp2, matches, None)
    
    # Resize logic (incase images are huge)
    # We resize to a fixed height of 600px to fit your screen
    h, w = result_img.shape[:2]
    new_h = 600
    scale = new_h / h
    new_w = int(w * scale)
    result_img = cv2.resize(result_img, (new_w, new_h))

    cv2.imshow(title, result_img)
    print(f"   >>> DISPLAYING: {title} (Press any key to continue...)")
    cv2.waitKey(0) # Waits for you to press a key
    cv2.destroyAllWindows()

# --- 3. Main Execution ---
def main():
    input_folder = "unknowns"
    database_folder = "database"
    valid_ext = ('.png', '.jpg', '.jpeg', '.bmp', '.tif', '.tiff')

    if not os.path.exists(input_folder):
        print(f"ERROR: '{input_folder}' missing.")
        return

    unknown_files = [f for f in os.listdir(input_folder) if f.lower().endswith(valid_ext)]
    
    print(f"--- STARTING VISUAL ANALYSIS ---")
    print(f"Processing {len(unknown_files)} images.\n")

    for u_file in unknown_files:
        print(f"🔎 Processing: {u_file}")
        
        u_path = os.path.join(input_folder, u_file)
        u_img = cv2.imread(u_path)
        if u_img is None: continue

        # -----------------------------------------
        # CHECK 1: DATABASE (Who is this?)
        # -----------------------------------------
        best_score = 0
        best_match_data = None # Stores (name, img, kp, mp)

        if os.path.exists(database_folder):
            for db_file in os.listdir(database_folder):
                if not db_file.lower().endswith(valid_ext): continue
                
                db_path = os.path.join(database_folder, db_file)
                db_img = cv2.imread(db_path)
                if db_img is None: continue

                score, kp1, kp2, good_points = get_match_details(u_img, db_img)
                
                if score > best_score:
                    best_score = score
                    # Save data so we can draw it later
                    best_match_data = (db_file, db_img, kp2, good_points, kp1)

        # REPORT & SHOW DATABASE RESULT
        if best_score > 20:
            name, db_img, db_kp, matches, u_kp = best_match_data
            print(f"   ✅ MATCH FOUND: {name} (Score: {best_score})")
            
            # SHOW THE IMAGE
            show_comparison(f"MATCH: {u_file} vs {name}", u_img, u_kp, db_img, db_kp, matches)
        else:
            print(f"   ❌ Unknown Identity.")

        # -----------------------------------------
        # CHECK 2: UNKNOWNS (Is there a copy here?)
        # -----------------------------------------
        for other_file in unknown_files:
            if other_file == u_file: continue 
            
            other_path = os.path.join(input_folder, other_file)
            other_img = cv2.imread(other_path)
            if other_img is None: continue

            score, kp1, kp2, good_points = get_match_details(u_img, other_img)
            
            if score > 20:
                print(f"   🔗 DUPLICATE FOUND: Same as '{other_file}' (Score: {score})")
                
                # SHOW THE IMAGE
                show_comparison(f"DUPLICATE: {u_file} vs {other_file}", u_img, kp1, other_img, kp2, good_points)

        print("-" * 50)

if __name__ == "__main__":
    main()
