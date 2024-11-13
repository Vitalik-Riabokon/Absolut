-- Видалення зовнішнього ключа (foreign key) з таблиці program_files
ALTER TABLE program_files
DROP CONSTRAINT program_files_program_id_fkey;

-- Додавання нового зовнішнього ключа (foreign key) до таблиці program_files
ALTER TABLE program_files
ADD CONSTRAINT program_files_program_id_fkey
FOREIGN KEY (program_id)  -- Вказується колонка program_id у таблиці program_files, яка є зовнішнім ключем
REFERENCES programs (program_id)  -- Вказується, що ця колонка посилається на колонку program_id у таблиці programs
ON DELETE CASCADE;  -- При видаленні запису з таблиці programs, всі пов'язані записи в program_files також будуть автоматично видалені
