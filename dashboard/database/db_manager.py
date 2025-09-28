"""Database connection and data loading utilities"""

import streamlit as st
import pandas as pd
import psycopg2
from psycopg2 import extras
from dotenv import load_dotenv
from os import environ as ENV
from config.settings import TABLES, CACHE_TTL

class DataManager:
    """Manages database connections and data loading"""
    
    def __init__(self):
        """Initialize database connection"""
        self.connection = self._init_connection()
    
    @st.cache_resource
    def _init_connection(_self):
        """Initialize PostgreSQL connection"""
        load_dotenv()
        return psycopg2.connect(
            dbname=ENV["DB_NAME"],
            host=ENV["DB_HOST"],
            user=ENV["DB_USER"],
            port=ENV["DB_PORT"],
            password=ENV["DB_PASSWORD"],
            cursor_factory=psycopg2.extras.RealDictCursor
        )
    
    @st.cache_data(ttl=CACHE_TTL)
    def _load_table(_self, table_name):
        """Load data from a specific table"""
        table_and_schema = f'analytics.{table_name}'
        query = f"SELECT * FROM {table_and_schema}"
        
        with _self.connection.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
        
        return pd.DataFrame(rows)
    
    def load_all_data(self):
        """Load all required tables"""
        data = {}
        
        for key, table_name in TABLES.items():
            try:
                data[key] = self._load_table(table_name)
            except Exception as e:
                st.error(f"Error loading {key}: {str(e)}")
                data[key] = pd.DataFrame()
        
        return data
    
    def get_table(self, table_key):
        """Get a specific table by key"""
        if table_key in TABLES:
            return self._load_table(TABLES[table_key])
        else:
            raise ValueError(f"Table key '{table_key}' not found")
    
    def close_connection(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()