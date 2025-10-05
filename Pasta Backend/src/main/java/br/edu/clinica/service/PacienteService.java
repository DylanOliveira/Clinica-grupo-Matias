package br.edu.clinica.service;

import br.edu.clinica.model.Paciente;
import br.edu.clinica.repository.PacienteRepository;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.time.Period;
import java.util.List;
import java.util.Optional;

@Service
public class PacienteService {

    private final PacienteRepository repo;

    public PacienteService(PacienteRepository repo) {
        this.repo = repo;
    }

    public Paciente salvar(Paciente p) {
        // Regra: se menor de 18 anos, precisa responsável
        if (p.getDataNasc() != null) {
            int idade = Period.between(p.getDataNasc(), LocalDate.now()).getYears();
            if (idade < 18 && (p.getNomeRespon() == null || p.getCpfRespon() == null)) {
                throw new IllegalArgumentException("Paciente menor de idade precisa de responsável!");
            }
        }
        return repo.save(p);
    }

    public List<Paciente> listar() {
        return repo.findAll();
    }

    public Optional<Paciente> buscarPorId(Long id) {
        return repo.findById(id);
    }

    public void remover(Long id) {
        repo.deleteById(id);
    }
}
