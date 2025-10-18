FROM node:20-alpine

WORKDIR /app

# Копируем package.json и package-lock.json
COPY package*.json ./

# Устанавливаем зависимости
RUN npm install

# Копируем весь фронтенд
COPY . .

# Открываем порт dev-сервера Vite
EXPOSE 5173

# Запуск dev-сервера
CMD ["npm", "run", "dev", "--", "--host"]
