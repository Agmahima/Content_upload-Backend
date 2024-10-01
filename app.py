import psycopg2
from flask import Flask, request, jsonify
import pandas as pd
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

UPLOAD_FOLDER = r'C:\Users\Prachi\Desktop\Backend_assignment'  
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

hostname = 'localhost'
database = 'Demo'
username = 'postgres'
pwd = 'Mahima@1208'
port_id = 5432

def connect_db():
    try:
        conn = psycopg2.connect(
            host=hostname,
            dbname=database,
            user=username,
            password=pwd,
            port=port_id
        )
        cur = conn.cursor()
        
        create_script = ''' 
        CREATE TABLE IF NOT EXISTS movie(
            id SERIAL PRIMARY KEY,
            budget INT,
            homepage VARCHAR(255),
            original_language VARCHAR(10),
            original_title VARCHAR(255),
            overview TEXT,
            release_date DATE,
            revenue BIGINT,
            runtime INT,
            status VARCHAR(50),
            title VARCHAR(255),
            vote_average FLOAT,
            vote_count INT,
            production_company_id VARCHAR(255),
            genre_id VARCHAR(255),
            languages VARCHAR(255)
        )
        '''
        cur.execute(create_script)
        conn.commit()
        
        return conn, cur
    
    except Exception as error:
        print(f"Error connecting to the database: {error}")
        return None, None

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and file.filename.endswith('.csv'):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            df = pd.read_csv(filepath)

            # Clean and convert release_date column
            if 'release_date' in df.columns:
                # Convert to datetime and coerce errors to NaT (Not a Time)
                df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')

                # Optionally handle NaT values (e.g., drop or fill)
                if df['release_date'].isnull().any():
                    # For example, drop rows with NaT values in release_date
                    df = df.dropna(subset=['release_date'])
            columns = df.columns.tolist()
            print("CSV Columns:", columns)  # Log the CSV columns
            
            expected_columns = [
                'budget', 'homepage', 'original_language', 'original_title', 
                'overview', 'release_date', 'revenue', 'runtime', 
                'status', 'title', 'vote_average', 'vote_count', 
                'production_company_id', 'genre_id', 'languages'
            ]
            
            if not set(expected_columns).issubset(set(columns)):
                return jsonify({'error': 'CSV columns do not match the database table'}), 400
            
            placeholders = ', '.join(['%s'] * len(columns))
            columns_sql = ', '.join(columns)
            insert_query = f'''
            INSERT INTO movie ({columns_sql})
            VALUES ({placeholders})
            '''
            
            conn, cur = connect_db()
            if conn is None or cur is None:
                return jsonify({'error': 'failed to connect to database'}), 500
            
            for _, row in df.iterrows():
                cur.execute(insert_query, tuple(row))
            
            conn.commit()
            return jsonify({'message': 'File uploaded successfully'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    else:
        return jsonify({'error': 'Only CSV files are allowed'}), 400


@app.route('/movies',methods=['GET'])
def get_movies():
    page=request.args.get('page',default=1,type=int)
    per_page=request.args.get('per_page',default=10,type=int)
    sort_by=request.args.get('sort_by',default='id',type=str)
    sort_order = request.args.get('sort_order', default='asc', type=str)
    filter_by = request.args.get('filter_by', default=None, type=str)
    filter_value = request.args.get('filter_value', default=None, type=str)
    
    conn,cur=connect_db()
    if conn is None or cur is None:
        return jsonify({'error': 'failed to connect to database'}), 500
    
    try:
        query="SELECT * FROM movie "
        
        if filter_by and filter_value:
            query+=f"WHERE {filter_by} ILIKE %s "
            filter_value=f"%{filter_value}% "
        query+=f"ORDER BY {sort_by} {sort_order} "
        
        offset = (page - 1) * per_page
        query += f" LIMIT %s OFFSET %s "
        
        if filter_by and filter_value:
            cur.execute(query, (filter_value, per_page, offset))
        
            
        else:
            cur.execute(query, (per_page, offset))
            
    
            
        movies = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        movies_list = [dict(zip(columns, movie)) for movie in movies]
        
        cur.execute("SELECT COUNT(*) FROM movie ")
        total_count = cur.fetchone()[0]

        return jsonify({
            'total_count': total_count,
            'page': page,
            'per_page': per_page,
            'movies': movies_list
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cur.close()
        conn.close()
        

if __name__ == '__main__':
    app.run(debug=True)
