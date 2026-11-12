import { defineConfig } from 'vitest/config'
export default defineConfig({ test: { include: ['../tests/frontend/**/*.test.ts'], root: '.' }, resolve: { alias: { '@': __dirname } } })
