def create_table(cur):
    """Создание таблиц при первом подключении"""
    cur.execute("""
                CREATE TABLE IF NOT EXISTS article (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_article TEXT UNIQUE,
                    url_article TEXT,
                    title_original_article TEXT,
                    text_original_article TEXT,
                    title_neiro_article TEXT DEFAULT NULL,
                    text_neiro_article TEXT DEFAULT NULL,
                    prompt_image TEXT,
                    time_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_view BOOLEAN DEFAULT FALSE,
                    is_published BOOLEAN DEFAULT FALSE
                )
            """)

    cur.execute(
        """
                CREATE TABLE IF NOT EXISTS image (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_article TEXT UNIQUE,                                
                    image_url TEXT DEFAULT NULL,
                    image_path TEXT DEFAULT NULL,
                    image_path_with_text TEXT DEFAULT NULL,
                    image_text TEXT DEFAULT NULL,        
                    is_published BOOLEAN DEFAULT FALSE
                    )
                """)
