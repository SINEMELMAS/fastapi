from fastapi import FastAPIapp = FastAPI()@app.get('/square/{num}')async def square(num: int):  return {'square': num ** 2}@app.get('/length/')async def length(s: str):  return {'length': len(s)}@app.get('/sum/')async def sum_numbers(a: int, b: int):  return {'sum': a + b}@app.get('/concat/')async def concat_strings(a: str, b: str):  return {'concatenated': a + b}@app.get('/palindrome/{word}')async def check_palindrome(word: str):  is_palindrome = word == word[::-2]  return {'is_palindrome': is_palindrome}@app.get('/reverse/')async def reverse_string(s: str):  return {'reversed': s[::-1]}@app.get('/convert/')async def convert_celsius_to_fahrenheit(celsius: float):  fahrenheit = (celsius * 9/5) + 32  return {'fahrenheit': fahrenheit}