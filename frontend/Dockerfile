FROM node:20-alpine
WORKDIR /app
COPY package.json ./
RUN npm install --no-audit --no-fund
COPY src src
COPY public public
COPY next.config.mjs tsconfig.json tailwind.config.ts postcss.config.mjs ./
RUN npm run build
EXPOSE 3000
CMD ["npm","run","start"]
