from pydantic_settings import BaseSettings,SettingsConfigDict
class Settings(BaseSettings):
 app_name:str="ST Insurance Pool API"; app_env:str="development"; database_url:str="sqlite:///./st_pool.db"
 ollama_base_url:str="http://localhost:11434"; ollama_model:str="qwen2.5:0.5b"; ollama_timeout:int=300
 model_config=SettingsConfigDict(env_file=".env",extra="ignore")
settings=Settings()
