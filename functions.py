import os
import mimetypes
from docx import Document
import PyPDF2

def handle_document (file_path: str) -> str:
    # Определяем MIME-тип файла
    mime_type = mimetypes.guess_type(file_path)[0]
    
    text = ""
    
    if mime_type == 'text/plain':
        # Обработка текстового файла (.txt)
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    elif mime_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        # Обработка .docx файла
        doc = Document(file_path)
        text = '\n'.join([para.text for para in doc.paragraphs])
    elif mime_type == 'application/pdf':
    # Обработка .pdf файла
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ''
            for page_num in range(len(reader.pages)):  # Используем len(reader.pages) вместо reader.numPages
                page = reader.pages[page_num]  # Получаем страницу по индексу
                text += page.extract_text() or ''  # Добавляем текст страницы или пустую строку, если текст не извлекается
    else:
        print("Не поддерживаемый тип файла.")
        os.remove(file_path)
        return
    
    # Удаляем файл после чтения
    os.remove(file_path)
    return text
  
def split_text(text: str, max_length: int = 1000) -> list:
    """Разделяет текст на части длиной не более max_length символов."""
    if max_length <= 0:
        raise ValueError("Максимальная длина должна быть больше нуля.")
    
    words = text.split()
    current_part = []
    current_length = 0
    result = []

    for word in words:
        # Проверяем, можно ли добавить слово к текущей части без превышения максимальной длины
        if current_length + len(word) + len(current_part) <= max_length:
            current_part.append(word)
            current_length += len(word)
        else:
            # Если слово не помещается, отправляем текущую часть в результат и начинаем новую часть с этого слова
            result.append(' '.join(current_part))
            current_part = [word]
            current_length = len(word)

    # Если остались слова в current_part, добавляем их в результат
    if current_part:
        result.append(' '.join(current_part))

    return result