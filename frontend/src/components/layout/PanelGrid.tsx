"use client"
import { DndContext, closestCenter } from "@dnd-kit/core"
import { SortableContext, arrayMove, rectSortingStrategy, useSortable } from "@dnd-kit/sortable"
import { CSS } from "@dnd-kit/utilities"
import { useState } from "react"

function SortablePanel({ panel }: { panel: { id: string; title: string; content: React.ReactNode } }) {
  const { attributes, listeners, setNodeRef, transform, transition } = useSortable({ id: panel.id })
  const style = { transform: CSS.Transform.toString(transform), transition }
  return (
    <div ref={setNodeRef} style={style} {...attributes} {...listeners} className="glass rounded-2xl p-4 min-h-[240px]">
      <div className="text-sm text-slate-400 mb-3">{panel.title}</div>
      {panel.content}
    </div>
  )
}

export function PanelGrid({ panels }: { panels: { id: string; title: string; content: React.ReactNode }[] }) {
  const [items, setItems] = useState(panels.map(p => p.id))
  const panelMap = panels.reduce((acc, panel) => ({ ...acc, [panel.id]: panel }), {} as Record<string, (typeof panels)[number]>)

  return (
    <DndContext
      collisionDetection={closestCenter}
      onDragEnd={event => {
        const { active, over } = event
        if (over && active.id !== over.id) {
          const oldIndex = items.indexOf(String(active.id))
          const newIndex = items.indexOf(String(over.id))
          setItems(arrayMove(items, oldIndex, newIndex))
        }
      }}
    >
      <SortableContext items={items} strategy={rectSortingStrategy}>
        <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
          {items.map(id => (
            <SortablePanel key={id} panel={panelMap[id]} />
          ))}
        </div>
      </SortableContext>
    </DndContext>
  )
}
