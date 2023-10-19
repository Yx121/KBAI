from SemanticNetsAgent import SemanticNetsAgent

def test():
    #This will test your SemanticNetsAgent
	#with seven initial test cases.
    test_agent = SemanticNetsAgent()

    print(test_agent.solve(1, 1))
    print(test_agent.solve(2, 2))
    print(test_agent.solve(3, 3))
    print(test_agent.solve(5, 3))
    print(test_agent.solve(6, 3))
    print(test_agent.solve(7, 3))
    print(test_agent.solve(5, 5))

if __name__ == "__main__":
    test()



import os
import shutil
src = r'D:\test1'
dst = r'D:\test2'
folder_ids_to_move = [123, 789]

for folder_id in folder_ids_to_move:
    folder = f'run_id_{folder_id}'
    src_folder_path = os.path.join(src, folder)
    dest_folder_path = os.path.join(dst, folder)
    if os.path.exists(src_folder_path):
        shutil.copytree(src_folder_path, dest_folder_path)
        print(f"Copied {folder} to {dst}")
    else:
        print(f"{folder} does not exist in {src}")