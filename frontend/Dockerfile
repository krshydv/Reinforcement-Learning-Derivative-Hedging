FROM node:20-alpine
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY src src
COPY public public
COPY next.config.mjs tsconfig.json tailwind.config.ts postcss.config.mjs ./
RUN npm run build
EXPOSE 3000
CMD ["npm","run","start"]
