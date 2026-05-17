import http from './index'

// 文档列表
export function fetchDocuments(params = {}) {
  return http.get('/documents', { params })
}

// 文档详情
export function getDocument(id) {
  return http.get(`/documents/${id}`)
}

// 创建文档
export function createDocument(data) {
  return http.post('/documents', data)
}

// 更新文档
export function updateDocument(id, data) {
  return http.put(`/documents/${id}`, data)
}

// 删除文档
export function deleteDocument(id) {
  return http.delete(`/documents/${id}`)
}

// 批量删除
export function batchDeleteDocuments(ids) {
  return http.post('/documents/batch-delete', ids)
}

// 统计概览
export function getStatsOverview(month) {
  return http.get('/stats/overview', { params: { month } })
}

// AI 转化
export function aiTransform(content) {
  return http.post('/ai/transform', { content })
}

// AI 转化并入库
export function aiTransformSave(docId) {
  return http.post(`/ai/transform/${docId}`)
}
