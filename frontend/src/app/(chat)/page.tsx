"use client";

import { ChatLayout } from "@/components/chat/chat-layout";
import {
  Dialog,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogContent,
} from "@/components/ui/dialog";
import UsernameForm from "@/components/username-form";
import { generateUUID } from "@/lib/utils";
import React from "react";
import useChatStore from "../hooks/useChatStore";

export default function Home() {
  const id = generateUUID();
  const [open, setOpen] = React.useState(false);
  const userName = useChatStore((state) => state.userName);
  const setUserName = useChatStore((state) => state.setUserName);

  const onOpenChange = (isOpen: boolean) => {
    if (userName) return setOpen(isOpen);

    setUserName("Anonyme");
    setOpen(isOpen);
  };

  return (
    <main className="flex h-[calc(100dvh)] flex-col items-center ">
      <Dialog open={open} onOpenChange={onOpenChange}>
        <ChatLayout
          key={id}
          id={id}
          initialMessages={[]}
          navCollapsedSize={10}
          defaultLayout={[30, 160]}
        />
        <DialogContent className="flex flex-col space-y-4">
          <DialogHeader className="space-y-2">
          <DialogTitle>Kairn — Votre repère dans le cloud souverain européen.</DialogTitle>
          <DialogDescription className="space-y-2">
            <p>
              Entrez votre nom pour commencer. Cet assistant vous aide à comprendre, explorer et utiliser les technologies du
              <strong> cloud souverain français</strong> — OVHcloud, Scaleway, infra open source et pratiques DevOps.
            </p>
            <p className="text-xs text-muted-foreground bg-muted/50 p-2 rounded">
              <strong>Utilisation des données</strong> :
              Nous ne sauvegardons pas vos interactions avec Kairn (vos chats sont stockées dans votre navigateur). 
              L'utilisation de Kairn implique l'utilisation du service API de Mistral AI qui est hébergé en EU.
            </p>
          </DialogDescription>


            <UsernameForm setOpen={setOpen} />
          </DialogHeader>
        </DialogContent>
      </Dialog>
    </main>
  );
}
