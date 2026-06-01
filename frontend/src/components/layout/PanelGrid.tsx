"use client"
import React, { useState } from "react"
import { DndContext, closestCenter } from "@dnd-kit/core"
import { SortableContext, arrayMove, rectSortingStrategy, useSortable } from "@dnd-kit/sortable"
import { CSS } from "@dnd-kit/utilities"
import { GripVertical } from "lucide-react"
import { Panel } from "../ui/Panel"
import { cn } from "../../lib/utils"

function SortablePanel({
  panel
}: {
  panel: { id: string; title: string; subtitle?: string; action?: React.ReactNode; content: React.ReactNode; span?: "full" }
}) {
  const { attributes, listeners, setNodeRef, transform, transition, isDragging } = useSortable({ id: panel.id })
  const style = { transform: CSS.Transform.toString(transform), transition }

  return (
    <div ref={setNodeRef} style={style} className={cn(panel.span === "full" && "xl:col-span-2", isDragging && "z-10 opacity-90")}>
      <Panel
        title={panel.title}
        subtitle={panel.subtitle}
        action={
          <button type="button" className="text-ink-faint hover:text-ink-secondary" {...attributes} {...listeners} aria-label="Drag panel">
            <GripVertical size={14} />
          </button>
        }
      >
        {panel.content}
      </Panel>
    </div>
  )
}

export function PanelGrid({
  panels
}: {
  panels: { id: string; title: string; subtitle?: string; action?: React.ReactNode; content: React.ReactNode; span?: "full" }[]
}) {
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
        <div className="grid grid-cols-1 gap-4 xl:grid-cols-2 xl:gap-5">
          {items.map(id => (
            <SortablePanel key={id} panel={panelMap[id]} />
          ))}
        </div>
      </SortableContext>
    </DndContext>
  )
}
