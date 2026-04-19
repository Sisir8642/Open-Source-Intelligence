'use client'
import React, { createContext, useContext, useReducer, useCallback } from 'react'
import type { Search, SearchSummary, SearchRequest } from '@/types'
import { searchAPI } from '@/lib/api'
import toast from 'react-hot-toast'

interface OSINTState {
  currentSearch: Search | null
  history: SearchSummary[]
  isSearching: boolean
  isLoadingHistory: boolean
  error: string | null
}

const initialState: OSINTState = {
  currentSearch: null,
  history: [],
  isSearching: false,
  isLoadingHistory: false,
  error: null,
}

type Action =
  | { type: 'SEARCH_START' }
  | { type: 'SEARCH_SUCCESS'; payload: Search }
  | { type: 'SEARCH_FAIL'; payload: string }
  | { type: 'SET_HISTORY'; payload: SearchSummary[] }
  | { type: 'SET_LOADING_HISTORY'; payload: boolean }
  | { type: 'SET_CURRENT_SEARCH'; payload: Search }
  | { type: 'DELETE_SEARCH'; payload: string }
  | { type: 'CLEAR_ERROR' }

function reducer(state: OSINTState, action: Action): OSINTState {
  switch (action.type) {
    case 'SEARCH_START':
      return { ...state, isSearching: true, error: null, currentSearch: null }
    case 'SEARCH_SUCCESS':
      return {
        ...state,
        isSearching: false,
        currentSearch: action.payload,
        history: [
          {
            id: action.payload.id,
            query: action.payload.query,
            entity_type: action.payload.entity_type,
            status: action.payload.status,
            risk_level: action.payload.risk_level,
            risk_score: action.payload.risk_score,
            created_at: action.payload.created_at,
            finding_count: action.payload.findings?.length ?? 0,
          },
          ...state.history.filter(h => h.id !== action.payload.id),
        ],
      }
    case 'SEARCH_FAIL':
      return { ...state, isSearching: false, error: action.payload }
    case 'SET_HISTORY':
      return { ...state, history: action.payload }
    case 'SET_LOADING_HISTORY':
      return { ...state, isLoadingHistory: action.payload }
    case 'SET_CURRENT_SEARCH':
      return { ...state, currentSearch: action.payload }
    case 'DELETE_SEARCH':
      return { ...state, history: state.history.filter(h => h.id !== action.payload) }
    case 'CLEAR_ERROR':
      return { ...state, error: null }
    default:
      return state
  }
}

interface OSINTContextValue extends OSINTState {
  runSearch: (payload: SearchRequest) => Promise<Search | null>
  loadHistory: () => Promise<void>
  loadSearch: (id: string) => Promise<void>
  deleteSearch: (id: string) => Promise<void>
  clearError: () => void
}

const OSINTContext = createContext<OSINTContextValue | null>(null)

export function OSINTProvider({ children }: { children: React.ReactNode }) {
  const [state, dispatch] = useReducer(reducer, initialState)

  const runSearch = useCallback(async (payload: SearchRequest): Promise<Search | null> => {
    dispatch({ type: 'SEARCH_START' })
    try {
      const search = await searchAPI.create(payload)
      dispatch({ type: 'SEARCH_SUCCESS', payload: search })
      toast.success(`Found ${search.findings?.length ?? 0} intelligence points`)
      return search
    } catch (err: unknown) {
      const msg = (err as { response?: { data?: { detail?: string } }; message?: string })
        ?.response?.data?.detail || 'Search failed. Please try again.'
      dispatch({ type: 'SEARCH_FAIL', payload: msg })
      toast.error(msg)
      return null
    }
  }, [])

  const loadHistory = useCallback(async () => {
    dispatch({ type: 'SET_LOADING_HISTORY', payload: true })
    try {
      const history = await searchAPI.list()
      dispatch({ type: 'SET_HISTORY', payload: history })
    } catch {
      toast.error('Failed to load search history')
    } finally {
      dispatch({ type: 'SET_LOADING_HISTORY', payload: false })
    }
  }, [])

  const loadSearch = useCallback(async (id: string) => {
    try {
      const search = await searchAPI.get(id)
      dispatch({ type: 'SET_CURRENT_SEARCH', payload: search })
    } catch {
      toast.error('Failed to load search')
    }
  }, [])

  const deleteSearch = useCallback(async (id: string) => {
    try {
      await searchAPI.delete(id)
      dispatch({ type: 'DELETE_SEARCH', payload: id })
      toast.success('Search deleted')
    } catch {
      toast.error('Failed to delete search')
    }
  }, [])

  const clearError = useCallback(() => dispatch({ type: 'CLEAR_ERROR' }), [])

  return (
    <OSINTContext.Provider value={{ ...state, runSearch, loadHistory, loadSearch, deleteSearch, clearError }}>
      {children}
    </OSINTContext.Provider>
  )
}

export function useOSINT() {
  const ctx = useContext(OSINTContext)
  if (!ctx) throw new Error('useOSINT must be used within OSINTProvider')
  return ctx
}
