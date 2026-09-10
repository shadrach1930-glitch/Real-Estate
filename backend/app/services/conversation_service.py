"""Conversation and message handling."""

from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.conversation import Conversation, Message
from app.models.customer import Customer
from app.models.enums import Channel, SenderType
from app.schemas.customer import CustomerCreate


class ConversationService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_or_create_customer(self, data: CustomerCreate | None) -> Customer:
        if data and data.phone:
            result = await self.db.execute(
                select(Customer).where(Customer.phone == data.phone)
            )
            existing = result.scalar_one_or_none()
            if existing:
                # Update missing fields
                if data.name and not existing.name:
                    existing.name = data.name
                if data.email and not existing.email:
                    existing.email = data.email
                await self.db.flush()
                return existing

        customer = Customer(
            name=data.name if data else None,
            email=data.email if data else None,
            phone=data.phone if data else None,
        )
        self.db.add(customer)
        await self.db.flush()
        return customer

    async def get_or_create_conversation(
        self,
        *,
        conversation_id: UUID | None,
        customer: Customer,
        channel: Channel = Channel.WEB,
    ) -> Conversation:
        if conversation_id:
            result = await self.db.execute(
                select(Conversation)
                .options(selectinload(Conversation.messages))
                .where(Conversation.id == conversation_id)
            )
            conv = result.scalar_one_or_none()
            if conv:
                return conv

        conv = Conversation(
            customer_id=customer.id,
            session_id=str(uuid4()),
            channel=channel,
        )
        self.db.add(conv)
        await self.db.flush()
        return conv

    async def add_message(
        self,
        conversation: Conversation,
        *,
        sender_type: SenderType,
        content: str,
    ) -> Message:
        message = Message(
            conversation_id=conversation.id,
            sender_type=sender_type,
            content=content,
        )
        self.db.add(message)
        await self.db.flush()
        return message

    async def get_conversation(self, conversation_id: UUID) -> Conversation | None:
        result = await self.db.execute(
            select(Conversation)
            .options(selectinload(Conversation.messages))
            .where(Conversation.id == conversation_id)
        )
        return result.scalar_one_or_none()
