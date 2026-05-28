import { defineStore } from 'pinia'
import { ref } from 'vue'
import * as api from '@/api/document'

export const useDocumentsStore = defineStore('documents', () => {
  const documents = ref([])
  const loading = ref(false)

  async function fetchDocuments(params = {}) {
    loading.value = true
    try {
      const { data } = await api.fetchDocuments(params)
      documents.value = data
    } finally {
      loading.value = false
    }
  }

  async function addDocument(doc) {
    const { data } = await api.createDocument({
      title: doc.title || '',
      content: doc.content || '',
      tags: Array.isArray(doc.tags) ? doc.tags.join(',') : (doc.tags || ''),
      ai_notes: doc.ai_notes || null,
      ai_mindmap: doc.ai_mindmap || null,
    })
    documents.value.unshift(data)
    return data
  }

  async function removeDocument(id) {
    await api.deleteDocument(id)
    documents.value = documents.value.filter((d) => d.id !== id)
  }

  async function updateTitle(id, title) {
    await api.updateDocument(id, { title })
    const doc = documents.value.find((d) => d.id === id)
    if (doc) doc.title = title
  }

  return { documents, loading, fetchDocuments, addDocument, removeDocument, updateTitle }
})
