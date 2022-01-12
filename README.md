# Duplicate File Handler
Users can delete duplicate files using this program. 

## How to use 
- run the file with argument of which folder to check. e.g. `python handler.py root_folder`
- Follow the instruction of the program, including:
  - Enter file format: input optional. Check for all file formats if input is empty.
  - Select file size sorting options: 1 or 2
  - Check for duplicates: yes for checking no for not checking
  - Delete files: yes for deleting no for not deleting
  - Enter file numbers to delete: input required.

## Theory
1. Check files of same sizes
2. Check files of same hash values.

## Example process
``` 
> python handler.py root_folder

Enter file format:
>

Size sorting options:
1. Descending
2. Ascending

Enter a sorting option:
> 1

5550640 bytes
root_folder/poker_face.mp3
root_folder/poker_face_copy.mp3

4590560 bytes
root_folder/gordon_ramsay_chicken_breast.avi
root_folder/audio/sia_snowman.mp3
root_folder/audio/rock/smells_like_teen_spirit.mp3

3422208 bytes
root_folder/audio/classic/unknown.mp3
root_folder/masterpiece/rick_astley_never_gonna_give_you_up.mp3

Check for duplicates?
> yes

5550640 bytes
Hash: 909ba4ad2bda46b10aac3c5b7f01abd5
1. root_folder/poker_face.mp3
2. root_folder/poker_face_copy.mp3

3422208 bytes
Hash: a7f5f35426b927411fc9231b56382173
3. root_folder/audio/classic/unknown.mp3
4. root_folder/masterpiece/rick_astley_never_gonna_give_you_up.mp3

Delete files?
> yes

Enter file numbers to delete:
> 1 2 9

Wrong format

Enter file numbers to delete:
> 1 2 4

Total freed up space: 14523488 bytes
```


Disclaimer: The original project idea is from [JetBrains Academy](https://hyperskill.org/projects/176). All codes were written by myself.