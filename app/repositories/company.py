from uuid import UUID

from schemas import Company, User

from .base import BaseRepository, InterfaceRepository


class CompanyRepository(BaseRepository, InterfaceRepository):

    def list(self, params):
        query = self.db.query(Company)
        query = self.filter(query, Company, params)
        query = self.search(query, Company, params)
        query = self.sort(query, Company, params)
        query = self.paginate(query, params)
        return query.all()

    def show(self, id: UUID):
        return self.db.query(Company).filter(Company.id == id).first()

    def get_company_users(self, company_id: UUID):
        return self.db.query(User).filter(User.company_id == company_id).all()
