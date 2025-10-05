package br.edu.clinica.service;

import br.edu.clinica.model.Procedimento;
import br.edu.clinica.repository.ProcedimentoRepository;
import br.edu.clinica.repository.AtendimentoRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class ProcedimentoService {

    private final ProcedimentoRepository repo;
    private final AtendimentoRepository atendimentoRepo;

    public ProcedimentoService(ProcedimentoRepository repo, AtendimentoRepository atendimentoRepo) {
        this.repo = repo;
        this.atendimentoRepo = atendimentoRepo;
    }

    public Procedimento salvar(Procedimento p) {
        return repo.save(p);
    }

    public List<Procedimento> listar() {
        return repo.findAll();
    }

    public void remover(Long id) {
        Procedimento p = repo.findById(id).orElseThrow();
        if (atendimentoRepo.existsByProcedimentosContaining(p)) {
            throw new IllegalArgumentException("Não é possível remover procedimento vinculado a atendimentos!");
        }
        repo.delete(p);
    }
}
